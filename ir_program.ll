; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare i32 @"length"()

declare void @"print_row_or_column"([25 x i8]* %".1", i32 %".2", i32 %".3")

declare [25 x i8] @"read_string"()

declare void @"print_table"([25 x i8]* %".1", i32 %".2", i32 %".3")

define double @"mean"([25 x i8]* %".1")
{
entry:
  %".3" = alloca double
  store double 0x402ae8240b780347, double* %".3"
  ret double 0x402ae8240b780347
}

define i32 @"run_llvmlite_compiler"()
{
entry:
  %".2" = alloca [3 x [25 x i8]]
  store [3 x [25 x i8]] [[25 x i8] c"\2234\22\00                    ", [25 x i8] c"\2245\22\00                    ", [25 x i8] c"\2245\22\00                    "], [3 x [25 x i8]]* %".2"
  %".4" = alloca double
  store double 0x3ff0000000000000, double* %".4"
  %".6" = bitcast [3 x [25 x i8]]* %".2" to [25 x i8]*
  %".7" = call double @"mean"([25 x i8]* %".6")
  store double %".7", double* %".4"
  %".9" = load double, double* %".4"
  %".10" = alloca [6 x i8]
  store [6 x i8] c"%.3f\0a\00", [6 x i8]* %".10"
  %".12" = bitcast [6 x i8]* %".10" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", double %".9")
  ret i32 0
}
