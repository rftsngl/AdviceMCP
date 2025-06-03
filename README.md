# project-mcp
[![smithery badge](https://smithery.ai/badge/@rftsngl/project-mcp)](https://smithery.ai/server/@rftsngl/project-mcp)
Bu proje, rastgele tavsiyeler sunan bir MCP (Model Context Protocol) sunucusudur.

## Özellikler

- MCP protokolü desteği (2024-11-05 versiyonu)
- Rastgele tavsiye API'si entegrasyonu
- Smithery uyumluluğu
- Docker desteği

## Kurulum

Docker ile:

```bash
# Docker imajını çek
docker pull rftsngl/project-mcp:latest

# Konteynerı çalıştır
docker run -d -p 8080:8080 --name mcp-server rftsngl/project-mcp:latest
```

## Kullanım

Sunucu varsayılan olarak 8080 portunda çalışır. API'yi test etmek için:

```bash
curl http://localhost:8080/api/v1/recommendations
```

## Lisans

MIT
