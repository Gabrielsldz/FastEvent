from prisma import Prisma

prisma = Prisma()


async def connect_prisma():
    global prisma
    await prisma.connect()
