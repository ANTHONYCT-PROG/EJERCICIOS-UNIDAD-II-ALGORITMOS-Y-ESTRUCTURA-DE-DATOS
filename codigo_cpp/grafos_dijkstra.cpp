// Grafo dirigido ponderado y algoritmo de Dijkstra en C++
#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <climits>
#include <string>
using namespace std;

typedef pair<int, string> NodoPeso;

class Grafo {
    unordered_map<string, vector<NodoPeso>> adyacencia;
public:
    void agregarArista(const string& origen, const string& destino, int peso) {
        adyacencia[origen].push_back({peso, destino});
    }
    unordered_map<string, int> dijkstra(const string& inicio, unordered_map<string, string>& predecesor) {
        unordered_map<string, int> dist;
        for (const auto& par : adyacencia) dist[par.first] = INT_MAX;
        dist[inicio] = 0;
        predecesor.clear();
        priority_queue<NodoPeso, vector<NodoPeso>, greater<NodoPeso>> heap;
        heap.push({0, inicio});
        while (!heap.empty()) {
            int d = heap.top().first;
            string u = heap.top().second;
            heap.pop();
            if (d > dist[u]) continue;
            for (const auto& par : adyacencia[u]) {
                int peso = par.first;
                string v = par.second;
                if (dist[v] > dist[u] + peso) {
                    dist[v] = dist[u] + peso;
                    predecesor[v] = u;
                    heap.push({dist[v], v});
                }
            }
        }
        return dist;
    }
    vector<string> caminoMinimo(const string& inicio, const string& fin, int& costo) {
        unordered_map<string, string> predecesor;
        auto dist = dijkstra(inicio, predecesor);
        costo = dist[fin];
        if (costo == INT_MAX) return {};
        vector<string> camino;
        string actual = fin;
        while (actual != inicio) {
            camino.push_back(actual);
            actual = predecesor[actual];
        }
        camino.push_back(inicio);
        reverse(camino.begin(), camino.end());
        return camino;
    }
};

int main() {
    Grafo g;
    g.agregarArista("A", "B", 1);
    g.agregarArista("A", "C", 4);
    g.agregarArista("B", "C", 2);
    g.agregarArista("B", "D", 5);
    g.agregarArista("C", "D", 1);
    cout << "Camino más corto de A a D:\n";
    int costo;
    vector<string> camino = g.caminoMinimo("A", "D", costo);
    for (size_t i = 0; i < camino.size(); ++i) {
        cout << camino[i];
        if (i + 1 < camino.size()) cout << " -> ";
    }
    cout << " (Costo: " << costo << ")" << endl;
    return 0;
} 