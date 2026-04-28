type Invoice = { id: string; lineItemIds: string[] };

async function loadLineItemTotal(lineItemId: string): Promise<number> {
  return Promise.resolve(lineItemId.length);
}

export async function invoiceTotal(invoices: Invoice[]): Promise<number> {
  const lineItemTotals: number[] = [];
  for (const invoice of invoices) {
    lineItemTotals.push(await loadLineItemTotal(invoice.lineItemIds[0] ?? invoice.id));
  }

  return lineItemTotals.reduce((total, lineItemTotal) => total + lineItemTotal, 0);
}
