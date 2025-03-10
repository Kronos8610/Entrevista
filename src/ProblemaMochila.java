import java.util.ArrayList;
import java.util.List;

public class ProblemaMochila {

    public static void main(String[] args) {
        // Pesos de los dispositivos
        int[] P = {4, 2, 1, 3}; 
        // Beneficios de los dispositivos
        int[] B = {2000, 1500, 1500, 2100}; 
        // Nombres de los dispositivos
        String[] dispositivos = {"Laptop", "Tablet", "Smartphone", "Cámara"};
        // Capacidad máxima de la mochila
        int W = 6; 

        // Llamada al método mochila para resolver el problema
        mochila(P, B, dispositivos, W);
    }

    // Método que resuelve el problema de la mochila utilizando programación dinámica
    public static int mochila(int[] P, int[] B, String[] dispositivos, int W) {
        // Número de dispositivos
        int N = P.length;
        
        // Creación de la matriz DP donde dp[i][w] representa el beneficio máximo 
        // con los primeros 'i' elementos y una capacidad máxima de mochila 'w'.
        int[][] dp = new int[N + 1][W + 1];

        // Rellenar la matriz DP
        for (int i = 1; i <= N; i++) {
            for (int w = 0; w <= W; w++) {
                // Si el peso del dispositivo i-1 es menor o igual a la capacidad 'w'
                if (P[i - 1] <= w) {
                    // Se toma el máximo entre no incluir el dispositivo i-1 o incluirlo
                    dp[i][w] = Math.max(dp[i - 1][w], B[i - 1] + dp[i - 1][w - P[i - 1]]);
                } else {
                    // Si el dispositivo i-1 no cabe, se mantiene el valor sin incluirlo
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        // Encontrar qué dispositivos fueron seleccionados
        List<String> seleccionados = new ArrayList<>();
        int w = W;
        
        // Recorrer la matriz desde el último dispositivo para encontrar los seleccionados
        for (int i = N; i > 0 && w > 0; i--) {
            // Si el valor cambia, significa que el dispositivo i-1 fue incluido
            if (dp[i][w] != dp[i - 1][w]) {
                // Añadir el dispositivo a la lista de seleccionados
                seleccionados.add(dispositivos[i - 1]);
                // Reducir la capacidad restante de la mochila
                w -= P[i - 1];
            }
        }

        // Imprimir el beneficio máximo obtenido
        System.out.println("Beneficio máximo: " + dp[N][W]);
        // Imprimir los dispositivos seleccionados en la mochila
        System.out.println("Dispositivos en la mochila: " + seleccionados);
        
        // Retorna el beneficio máximo
        return dp[N][W];
    }
}
