/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { rpc } from "@web/core/network/rpc";

const _super_setValue = OrderSummary.prototype._setValue;

patch(OrderSummary.prototype, {
    async _setValue(val) {
        const { numpadMode } = this.pos;
        let selectedLine = this.currentOrder.get_selected_orderline();

        if (selectedLine && numpadMode === "quantity" && val !== "remove") {
            const product = selectedLine.product_id;

            try {
                const quant = typeof val === "number" ? val : parseFloat("" + (val ? val : 0));
                const productId = product.id ?? product;

                const res = await rpc("/web/dataset/call_kw", {
                    model: "product.product",
                    method: "check_limit",
                    args: [productId],
                    kwargs: {},
                });

                if (res && res.has_limit && res.limit > 0) {
                    let totalOtherQty = 0;

                    for (const line of this.currentOrder.lines) {
                        if (line !== selectedLine && line.product_id?.id === product.id) {
                            totalOtherQty += Number(line.qty || 0);
                        }
                    }

                    const finalQty = totalOtherQty + quant;

                    if (finalQty > res.limit) {
                        this.env.services.notification.add(
                            `This product '${res.name}' has a limit of ${res.limit} per order.`,

                            {
                                title: "Quantity Limit Exceeded",
                                type: "warning",
                            }
                        );

                        this.numberBuffer.reset();
                        return;
                    }
                    console.log(res)
                }
            } catch (error) {
                console.error("Error in limit check:", error);
            }
        }

        return _super_setValue.call(this, val);
    },
});
