; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

define i32 @"run_llvmlite_compiler"()
{
entry:
  %"suka" = alloca double
  store double 0x40155c28f5c28f5c, double* %"suka"
  %".3" = load double, double* %"suka"
  %".4" = alloca [6 x i8]
  store [6 x i8] c"%.3f\0a\00", [6 x i8]* %".4"
  %".6" = load [6 x i8], [6 x i8]* %".4"
  %".7" = bitcast [6 x i8]* %".4" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", double %".3")
  ret i32 0
}

declare i32 @"printf"(i8* %".1", ...)
