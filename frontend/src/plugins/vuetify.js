import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                background: '#F5F5F5',
            }
        },
        options: {
            customProperties: true
        },
    }
});
