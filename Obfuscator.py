# Simple python code obfuscator
# Author: AirFlow
# Contact: https://airflowd.netlify.app/

import ast
import base64
import zlib
import random
import string
import re
import sys
import marshal
from io import StringIO

class CodeObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.string_cache = {}
        self.current_class = None
        self.import_aliases = {}
    
    def visit_Module(self, node):
        self.generic_visit(node)
        junk_nodes = self._generate_junk_code(3)
        node.body = junk_nodes + node.body
        return node
    
    def visit_FunctionDef(self, node):
        new_name = self._generate_random_name()
        self.func_map[node.name] = new_name
        node.name = new_name
        
        junk_nodes = self._generate_junk_code(2)
        node.body = junk_nodes + node.body
        
        self.generic_visit(node)
        return node
    
    def visit_ClassDef(self, node):
        new_name = self._generate_random_name()
        self.class_map[node.name] = new_name
        old_class = self.current_class
        self.current_class = node.name
        node.name = new_name
        
        junk_nodes = self._generate_junk_code(2)
        node.body = junk_nodes + node.body
        
        self.generic_visit(node)
        self.current_class = old_class
        return node
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) or isinstance(node.ctx, ast.Store):
            if node.id in self.var_map:
                node.id = self.var_map[node.id]
            elif node.id in self.func_map:
                node.id = self.func_map[node.id]
            elif node.id in self.class_map:
                node.id = self.class_map[node.id]
            elif self.current_class and f"{self.current_class}.{node.id}" in self.var_map:
                node.id = self.var_map[f"{self.current_class}.{node.id}"]
        return node
    
    def visit_Attribute(self, node):
        self.generic_visit(node)
        if isinstance(node.attr, str):
            if node.attr in self.var_map:
                node.attr = self.var_map[node.attr]
            elif node.attr in self.func_map:
                node.attr = self.func_map[node.attr]
        return node
    
    def visit_Constant(self, node):
        if isinstance(node.value, str):
            if node.value not in self.string_cache:
                self.string_cache[node.value] = self._encode_string(node.value)
            new_node = ast.Call(
                func=ast.Name(id='eval', ctx=ast.Load()),
                args=[ast.Constant(value=self.string_cache[node.value])],
                keywords=[]
            )
            return new_node
        return node
    
    def visit_Import(self, node):
        for alias in node.names:
            if alias.asname is None:
                new_name = self._generate_random_name()
                self.import_aliases[alias.name] = new_name
                alias.asname = new_name
            else:
                self.import_aliases[alias.name] = alias.asname
        return node
    
    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.asname is None:
                new_name = self._generate_random_name()
                self.import_aliases[f"{node.module}.{alias.name}"] = new_name
                alias.asname = new_name
            else:
                self.import_aliases[f"{node.module}.{alias.name}"] = alias.asname
        return node
    
class CodeObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.var_map = {}
        self.func_map = {}
        self.class_map = {}
        self.string_cache = {}
        self.current_class = None
        self.import_aliases = {}
    
    
    def _generate_random_name(self, length=12):
        chars = string.ascii_letters + string.digits
        while True:
            name = ''.join(random.choice(chars) for _ in range(length))
            if (name not in self.var_map.values() and 
                name not in self.func_map.values() and
                name not in self.class_map.values()):
                return name
    
    def _encode_string(self, s):
        """Modified to avoid dynamic imports"""
        encoded = base64.b64encode(zlib.compress(s.encode('utf-8'))).decode('utf-8')
        return f"zlib.decompress(base64.b64decode('{encoded}')).decode('utf-8')"
    
    def _generate_junk_code(self, count=1):
        junk_nodes = []
        for _ in range(count):
            junk_type = random.randint(0, 3)
            if junk_type == 0:
                var_name = self._generate_random_name()
                self.var_map[var_name] = var_name
                assign_node = ast.Assign(
                    targets=[ast.Name(id=var_name, ctx=ast.Store())],
                    value=ast.Constant(value=random.randint(0, 1000))
                )
                ast.fix_missing_locations(assign_node)
                junk_nodes.append(assign_node)
            elif junk_type == 1:
                if_node = ast.If(
                    test=ast.Compare(
                        left=ast.Constant(value=random.randint(0, 100)),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=random.randint(0, 100))]
                    ),
                    body=[ast.Pass()],
                    orelse=[]
                )
                ast.fix_missing_locations(if_node)
                junk_nodes.append(if_node)
            elif junk_type == 2:
                expr_node = ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id='print', ctx=ast.Load()),
                        args=[ast.Constant(value=''.join(random.choice(string.printable) for _ in range(10)))],
                        keywords=[]
                    )
                )
                ast.fix_missing_locations(expr_node)
                junk_nodes.append(expr_node)
            else:
                expr_node = ast.Expr(
                    value=ast.BinOp(
                        left=ast.Constant(value=''.join(random.choice(string.ascii_letters) for _ in range(5))),
                        op=ast.Add(),
                        right=ast.Constant(value=''.join(random.choice(string.ascii_letters) for _ in range(5)))
                    )
                )
                ast.fix_missing_locations(expr_node)
                junk_nodes.append(expr_node)
        return junk_nodes

def obfuscate_code(source_code):
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"Syntax error in source code: {e}")
        return None
    
    obfuscator = CodeObfuscator()
    obfuscated_tree = obfuscator.visit(tree)
    
    imports = [
        ast.Import(names=[ast.alias(name='base64', asname=None)]),
        ast.Import(names=[ast.alias(name='zlib', asname=None)])
    ]
    obfuscated_tree.body = imports + obfuscated_tree.body
    
    obfuscated_code = ast.unparse(obfuscated_tree)
    obfuscated_code = _obfuscate_with_marshal(obfuscated_code)
    obfuscated_code = _add_junk_comments(obfuscated_code)
    
    return obfuscated_code

def _obfuscate_with_marshal(code):
    """Modified wrapper to ensure proper imports"""
    try:
        code_obj = compile(code, '<string>', 'exec')
        marshaled = marshal.dumps(code_obj)
        encoded = base64.b64encode(zlib.compress(marshaled)).decode('utf-8')
        
        wrapper = """import base64, zlib, marshal
def _d(s):
    return marshal.loads(zlib.decompress(base64.b64decode(s)))
exec(_d('{encoded}'))
""".format(encoded=encoded)
        return wrapper
    except Exception as e:
        print(f"Warning: Marshal obfuscation failed: {e}")
        return code

def _add_junk_comments(code):
    lines = code.split('\n')
    obf_lines = []
    for line in lines:
        obf_lines.append(line)
        if random.random() > 0.7:
            junk_comment = '#' + ''.join([random.choice(string.printable) for _ in range(random.randint(10, 50))])


            obf_lines.append(junk_comment)
    return '\n'.join(obf_lines)

def main():
    if len(sys.argv) != 2:
        print("Usage: python obfuscator.py file.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.py', '_obfuscated.py')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        obfuscated_code = obfuscate_code(source_code)
        
        if obfuscated_code:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(obfuscated_code)
            print(f"Obfuscated code saved to {output_file}")
        else:
            print("Obfuscation failed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()