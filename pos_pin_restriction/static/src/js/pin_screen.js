/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class PosPinScreen extends Component {
    static template = "pos_pin_restriction.PinScreen";

    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.state = useState({
            pin: "",
            error: false,
        });
    }

    onKeyClick(key) {
        if (this.state.pin.length < 6) {
            this.state.pin += key;
            this.state.error = false;
        }
    }

    onBackspace() {
        this.state.pin = this.state.pin.slice(0, -1);
        this.state.error = false;
    }

    onClear() {
        this.state.pin = "";
        this.state.error = false;
    }

    async onEnter() {
        if (this.state.pin.length === 0) return;

        try {
            const result = await this.orm.call(
                'pos.config',
                'verify_pin_and_get_action',
                [this.state.pin]
            );

            if (result.error) {
                this.state.error = result.error;
                this.state.pin = "";
            } else if (result.action) {
                // Execute the returned action (Kanban view with domain)
                this.actionService.doAction(result.action);
            }
        } catch (error) {
            console.error("PIN Verification Error", error);
            this.state.error = "An error occurred during verification.";
        }
    }
}

registry.category("actions").add("pos_pin_restriction.pin_screen", PosPinScreen);
