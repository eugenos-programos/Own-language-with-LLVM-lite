; ModuleID = "/home/eug/Documents/ANTLR/src/number_operations.py"
target triple = "x86_64-linux-gnu"
target datalayout = ""

define double @"main"(double %".1", double %".2")
{
entry:
  %"res" = fadd double %".1", %".2"
  ret double %"res"
}
