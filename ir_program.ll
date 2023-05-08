; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

define i32 @"run_llvmlite_compiler"()
{
entry:
  %".2" = fadd double 0x4024cccccccccccd, 0x403d000000000000
  %".3" = bitcast [4 x i8]* @"fstr" to i8*
  %".4" = call i32 (i8*, ...) @"printf"(i8* %".3", double %".2")
  ret i32 0
}

@"fstr" = internal constant [4 x i8] c"%f\0a\00"
declare i32 @"printf"(i8* %".1", ...)
