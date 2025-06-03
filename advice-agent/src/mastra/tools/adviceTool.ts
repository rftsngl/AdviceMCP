import { createTool } from "@mastra/core/tools";
import { z } from "zod";

// ❶ Smithery MCP endpoint URL’ini buraya yazın
const SMITHERY_MCP_URL =
  "https://server.smithery.ai/@rftsngl/project-mcp/mcp?api_key=8b9eec3e-6cf6-46bc-bcd1-ec64501e6d1d";

// ❷ Girdi şeması: MCP çağrısı için method ve opsiyonel params
const inputSchema = z.object({
  method: z.string().describe("Çağrılacak uzak yöntem adı"),
  params: z.any().optional().describe("JSON-RPC parametreleri (opsiyonel)")
});

// ❸ Çıktı şeması: JSON-RPC yanıtı, result veya error içerir
const outputSchema = z.object({
  result: z.any().optional(),
  error: z.any().optional()
});

export const callMcpTool = createTool({
  id: "callSmitheryMCP",
  description: "Smithery MCP endpoint'ine JSON-RPC 2.0 çağrısı yapar",
  inputSchema,
  outputSchema,
  execute: async ({ context }) => {
    const { method, params } = context;
    // ❹ JSON-RPC 2.0 yükünü oluştur
    const rpcPayload = {
      jsonrpc: "2.0",
      id: Date.now(),    // benzersiz bir istek ID'si
      method,
      params: params ?? {}
    };
    // ❺ HTTP POST isteğini yap
    const resp = await fetch(SMITHERY_MCP_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(rpcPayload)
    });
    if (!resp.ok) {
      throw new Error(
        `MCP çağrısı başarısız: ${resp.status} ${resp.statusText}`
      );
    }
    const data = await resp.json();
    // ❻ JSON-RPC hata döndüyse maskele veya fırlat
    if (data.error) {
      throw new Error(`MCP Hatası: ${data.error.code} - ${data.error.message}`);
    }
    // ❼ Başarılı sonucu döndür
    return { result: data.result };
  }
});