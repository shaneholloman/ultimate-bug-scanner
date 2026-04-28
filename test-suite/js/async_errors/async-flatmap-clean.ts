type Order = { id: string; itemIds: string[] };

async function loadRecommendations(itemId: string): Promise<string[]> {
  return Promise.resolve([`${itemId}-primary`, `${itemId}-backup`]);
}

export async function recommendedItemIds(orders: Order[]): Promise<string[]> {
  try {
    const perOrderRecommendations: string[][] = [];
    for (const order of orders) {
      const recommendations = await loadRecommendations(order.itemIds[0] ?? order.id);
      perOrderRecommendations.push(recommendations);
    }

    return perOrderRecommendations.flatMap((itemIds) => itemIds);
  } catch (error) {
    throw new Error(`failed to load recommendations: ${String(error)}`);
  }
}
