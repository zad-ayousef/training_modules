/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { rpc } from "@web/core/network/rpc";

const _super_addProduct = ProductScreen.prototype.addProductToOrder;

patch(ProductScreen.prototype, {
    async addProductToOrder(product) {
        try {
            const currentQty = this._getCurrentQtyForProduct(product) || 0;
            const intendedDelta = 1;
            const finalQty = currentQty + intendedDelta;

            const productId = product && (product.id ?? product);
            const res = await rpc("/web/dataset/call_kw", {
                model: "product.product",
                method: "check_limit",
                args: [productId],
                kwargs: {},
            });

            if (res && res.has_limit && res.limit > 0 && finalQty > res.limit) {
                this.env.services.notification.add(
                    `This product '${res.name}' has a limit of ${res.limit} per order.`,
                    {
                        title: "Quantity Limit Exceeded",
                        type: "warning",
                    }
                );
                return;
            }

            return await _super_addProduct.apply(this, arguments);
        } catch (err) {
            console.error("Limit check failed (addProductToOrder):", err);
            return await _super_addProduct.apply(this, arguments);
        }
    },

    _getCurrentQtyForProduct(product) {
        try {
            const order = this.currentOrder;
            if (!order || !order.lines) return 0;
            let sum = 0;
            for (const line of order.lines) {
                const pid =
                    (line.product && (line.product.id ?? line.product)) ||
                    (line.product_id && (line.product_id.id ?? line.product_id)) ||
                    null;
                if (pid && pid === (product.id ?? product)) {
                    sum += Number(line.qty || 0);
                }
            }
            return sum;
        } catch (e) {
            console.error("Error computing current qty for product:", e);
            return 0;
        }
    },
});
