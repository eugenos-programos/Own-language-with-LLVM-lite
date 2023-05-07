import sys
import llvmlite.binding as llvm


# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one


if len(sys.argv) == 1:
    raise FileNotFoundError("Put file name in command line arguments")


with open(sys.argv[1], "r") as ir_code_file:
    llvm_ir = ir_code_file.read()


def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


from llvmlite import ir, binding

# Initialize LLVMlite
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

#
# Create the execution engine
target = binding.Target.from_default_triple()
target_machine = target.create_target_machine()
backing_mod = binding.parse_assembly(llvm_ir)
engine = binding.create_mcjit_compiler(backing_mod, target_machine)

# Compile the module
mod = binding.parse_assembly(llvm_ir)
engine.add_module(mod)
engine.finalize_object()

# Generate executable code
engine.finalize_object()
filename = "my_executable"
with open(filename, "wb") as file:
    file.write(engine)

print("Executable file generated:", filename)
