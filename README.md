# Projeto LCD e SDCard com CircuitPython para RP2040-GEEK

Este projeto é projetado especificamente para o microcontrolador RP2040-GEEK, utilizando um display LCD de 1.14 polegadas (240x135) da Waveshare. Ele exibe uma interface no LCD e lê arquivos de um cartão SD, executando scripts Python encontrados nele.

## Hardware Requerido

- **Microcontrolador:** RP2040-GEEK
- **Display LCD:** 1.14 polegadas, 240x135 pixels, da Waveshare
- **Cartão SD:** Formatado em FAT (para armazenamento de scripts Python)

## Instruções de Preparação

Para preparar seu RP2040-GEEK para este projeto, siga estas etapas em ordem:

1. **Limpeza da Flash:**
   - Primeiro, use o arquivo `flash_nuke.uf2` para limpar completamente a flash do microcontrolador. Isso garante que o dispositivo esteja limpo e pronto para uma nova instalação do CircuitPython.

2. **Instalação do CircuitPython:**
   - Após limpar a flash, use o arquivo `circuit.uf2` para instalar o CircuitPython no seu dispositivo. Esse passo é crucial para rodar o script fornecido.

3. **Configuração de Armazenamento:**
   - Por padrão, o armazenamento USB está habilitado. Para desabilitá-lo (o que é recomendado para evitar problemas durante a execução do script), renomeie o arquivo `boot.py.disable` para `boot.py`.
   - Caso deseje habilitar o armazenamento USB novamente, conecte-se ao console serial do dispositivo e execute os seguintes comandos:
     ```python
     import os
     os.rename('boot.py', 'boot.py.disable')
     ```

## Preparação do Cartão SD

- Certifique-se de que o cartão SD esteja formatado em FAT. Copie o script Python que você deseja executar na raiz do cartão SD.

## Script Principal

O script principal realiza as seguintes funções:

- Inicializa a comunicação SPI com o cartão SD e o LCD.
- Monta o sistema de arquivos do cartão SD.
- Lista e executa arquivos `.py` encontrados na raiz do cartão SD.
- Exibe informações no LCD, incluindo uma sequência de terminal simulada e arte personalizada.

## Estrutura do Código

O código contém classes para controle do LCD (`LCDController` e `EnhancedLCDController`) e uma classe para gerenciamento do cartão SD (`SDCard`). Ele demonstra a utilização de SPI, leitura de arquivos, execução de scripts Python, e exibição de textos e arte em um display LCD compatível com o RP2040-GEEK.

## Como Usar

1. Prepare o RP2040-GEEK, o display LCD da Waveshare e o cartão SD conforme as instruções acima.
2. Copie este script para o microcontrolador.
3. Reinicie o microcontrolador para começar a execução.

Lembre-se de que, para alterações no script ou no conteúdo do cartão SD, pode ser necessário desabilitar temporariamente o armazenamento USB para evitar conflitos.