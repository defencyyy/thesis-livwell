import mutations from "./mutations";
import actions from "./actions";
import getter from "./getter";
export default {
    namespaced: true,
    state() {
        return {
            name: ' Leela',
        };
    },
    mutations,
    getter,
    actions,
};