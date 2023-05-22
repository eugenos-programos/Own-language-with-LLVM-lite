; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"length"()

declare void @"print_row_or_column"([25 x i8]* %".1", i32 %".2", i32 %".3")

declare [25 x i8] @"read_string"()

declare void @"print_table"([25 x i8]* %".1", i32 %".2", i32 %".3")

define double @"mean"()
{
entry:
  %".2" = alloca double
  store double 0x402a000000000000, double* %".2"
  ret double 0x402a000000000000
}

define i32 @"run_llvmlite_compiler"()
{
entry:
  %".2" = alloca double
  store double 0x3ff0000000000000, double* %".2"
  %".4" = call double @"mean"()
  store double %".4", double* %".2"
  %".6" = load double, double* %".2"
  %".7" = alloca [6 x i8]
  store [6 x i8] c"%.3f\0a\00", [6 x i8]* %".7"
  %".9" = bitcast [6 x i8]* %".7" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", double %".6")
  ret i32 0
}
