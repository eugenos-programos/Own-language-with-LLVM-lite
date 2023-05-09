; ModuleID = ""
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"run_llvmlite_compiler"()
{
entry:
  %"a" = alloca [5 x i8]
  store [5 x i8] c"\22a_\22\00", [5 x i8]* %"a"
  %"b" = alloca [5 x i8]
  store [5 x i8] c"\22b_\22\00", [5 x i8]* %"b"
  %".4" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".4"
  %".6" = bitcast [4 x i8]* %".4" to i8*
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", [5 x i8]* %"a")
  %".8" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".8"
  %".10" = bitcast [4 x i8]* %".8" to i8*
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", [5 x i8]* %"b")
  %"a.1" = alloca [6 x i8]
  store [6 x i8] c"\22dfd\22\00", [6 x i8]* %"a.1"
  %".13" = alloca [4 x i8]
  store [4 x i8] c"%s\0a\00", [4 x i8]* %".13"
  %".15" = bitcast [4 x i8]* %".13" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15", [6 x i8]* %"a.1")
  ret i32 0
}
