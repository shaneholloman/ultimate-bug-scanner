type Order = { id: string; itemIds: string[] };

async function loadRecommendations(itemId: string): Promise<string[]> {
  return Promise.resolve([`${itemId}-primary`, `${itemId}-backup`]);
}

export async function recommendedItemIds(orders: Order[]) {
  return orders.flatMap(async (order) => {
    return loadRecommendations(order.itemIds[0] ?? order.id);
  });
}
