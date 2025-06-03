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

// filepath: mastra.config.js
export default {
  storage: {
    type: 'memory', // Geliştirme için 'memory' kullanabilirsiniz
    options: {}
  },
  // diğer yapılandırmalar...
}