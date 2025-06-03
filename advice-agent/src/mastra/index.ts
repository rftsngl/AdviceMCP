import { Mastra } from "@mastra/core";
import { adviceAgent } from "./agents/adviceAgent";

export const mastra = new Mastra({
  agents: { adviceAgent },
});

// ES module ortamı için ana dosya kontrolü:
// ES module ortamı için ana dosya kontrolü:
if (import.meta.url === process.argv[1] || import.meta.url === `file://${process.argv[1]}`) {
  // Mastra'nın başlatılması gerekiyorsa, ilgili fonksiyonu burada çağırın.
  // Örneğin, mastra.run() veya uygun başka bir fonksiyon.
  // Eğer doğrudan bir başlatma fonksiyonu yoksa, bu bloğu kaldırabilirsiniz.
  console.log("Mastra instance created:", mastra);
}
//3a9b4fe3-d407-414c-a38a-39412c82a576