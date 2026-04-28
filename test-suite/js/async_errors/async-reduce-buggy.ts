type Invoice = { id: string; lineItemIds: string[] };

async function loadLineItemTotal(lineItemId: string): Promise<number> {
  return Promise.resolve(lineItemId.length);
}

export async function invoiceTotal(invoices: Invoice[]): Promise<number> {
  return invoices.reduce(async (total, invoice) => {
    const lineItemTotal = await loadLineItemTotal(invoice.lineItemIds[0] ?? invoice.id);
    return total + lineItemTotal;
  }, 0);
}
