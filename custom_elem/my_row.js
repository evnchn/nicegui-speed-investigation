export default {
    template: `
        <div class="w-full columns-7 px-4 text-xs text-black font-bold text-center [&_*]:w-full">
            <template v-for="(text, index) in texts" :key="'header-' + index">
                {{ text }}
                <i 
                    :class="bools[index] ? 'text-red' : 'text-black'" 
                    class="q-icon notranslate material-icons text-sm" 
                    aria-hidden="true" 
                    role="presentation"
                >
                    {{ bools[index] ? 'radio_button_checked' : 'radio_button_unchecked' }}
                </i>
            </template>
        </div>
    `,
    props: {
        texts: {
            type: Array,
            default: () => [],
        },
        bools: {
            type: Array,
            default: () => [],
        },
    },
};