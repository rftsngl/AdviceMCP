import { createWorkflow } from "@mastra/core/workflow";
import { callMcpTool } from "../tools/adviceTool";

export const adviceWorkflow = createWorkflow({
  id: "adviceWorkflow",
  description: "Kullanıcıya rastgele bir nasihat (advice) getirir.",
  inputSchema: {}, // Girdi gerekmiyor
  steps: [
    {
      id: "getAdvice",
      tool: callMcpTool,
      input: {
        method: "tools.call",
        params: { name: "get_advice", arguments: {} }
      },
      outputMap: (result) => ({
        advice: result.result?.content?.[0]?.text ?? "Nasihat alınamadı."
      })
    }
  ],
  outputMap: (context) => ({
    advice: context.getAdvice.advice
  })
});