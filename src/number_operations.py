from llvmlite import ir
from llvmlite import binding as llvm


llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


module = ir.Module(name="llvm_module")
function_type = ir.FunctionType(ir.IntType(32), [], False)
function = ir.Function(module=module, ftype=function_type, name="number_sum")


entry_block = function.append_basic_block(name="func_block")
builder = ir.IRBuilder(entry_block)


constant1 = ir.Constant(ir.IntType(32), 10)
constant2 = ir.Constant(ir.IntType(32), 10)
result = builder.add(constant1, constant1)

builder.ret(result)

print(module)

with open("IR_code.ll", "w") as file:
    file.write(str(module))

