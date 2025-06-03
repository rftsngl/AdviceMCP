import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";
import { callMcpTool } from "../tools/adviceTool";

export const adviceAgent = new Agent({
  name: "SmitheryMCPAgent",
  instructions: `
    Kullanıcı "nasihat" istediğinde, get_advice aracını şu şekilde çağır:
      method: "tools/call"
      params: { name: "get_advice", arguments: {} }
    Sonuç olarak dönen nasihati kullanıcıya göster.
  `,
  model: openai("gpt-4"),
  tools: { callMcpTool }
});