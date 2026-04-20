import asyncio
import time


async def fazer_pedido_assincrono(id_pedido):
    print(f"[Async] Começando pedido {id_pedido}...")
    await asyncio.sleep(2)
    print(f"[Async] Pedido {id_pedido} pronto!")


async def executar_assincrono():
    print("Iniciando processo assíncrono...")
    inicio = time.time()

    await asyncio.gather(
        fazer_pedido_assincrono(1),
        fazer_pedido_assincrono(2),
        fazer_pedido_assincrono(3),
    )

    fim = time.time()
    print(f"Tempo total Assíncrono: {fim - inicio:.2f} segundos")


if __name__ == "__main__":
    asyncio.run(executar_assincrono())
