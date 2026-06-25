public class Fibonacci {
public static int iterativeFib(int n) {
int a = 0, b = 1;
for (int i = 0; i < n; i++) {
a = b;
b = a + b;
}
return a;
}}