export default {
    template: `
        <div class="w-full flex px-4 text-xs text-black text-center h-[32px]" ref="observerTarget">
            <template v-if="isVisible">
                <div class="flex w-full">
                    <div v-for="(text, index) in texts" :key="'header-' + index" class="font-bold text-center flex-grow basis-0">
                        {{ text }}
                    </div>
                </div>
                <div class="flex w-full">
                    <i v-for="(checked, index) in bools" :key="'row-' + index"
                        :class="checked ? 'text-red' : 'text-black'" 
                        class="q-icon notranslate material-icons text-sm flex-grow basis-0" 
                        aria-hidden="true" 
                        role="presentation"
                    >
                        {{ checked ? 'radio_button_checked' : 'radio_button_unchecked' }}
                    </i>
                </div>
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
        sensitivity: {
            type: Number,
            default: 0.5, // Default sensitivity is 1 times the innerHeight
        },
    },
    data() {
        return {
            isVisible: false,
            observer: null,
            useObserver: 'IntersectionObserver' in window,
            ticking: false,
        };
    },
    mounted() {
        if (this.useObserver) {
            this.createObserver();
        } else {
            this.checkVisibility();
            window.addEventListener('scroll', this.onScroll);
        }
    },
    beforeDestroy() {
        if (this.useObserver && this.observer) {
            this.observer.disconnect();
        } else {
            window.removeEventListener('scroll', this.onScroll);
        }
    },
    methods: {
        createObserver() {
            const options = {
                root: null, // Use the viewport as the root
                rootMargin: `${this.sensitivity * 100}%`, // Adjust margin based on sensitivity (percent)
                threshold: 0, // Trigger when any part of the target is visible
            };

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    this.isVisible = entry.isIntersecting;
                });
            }, options);

            this.observer.observe(this.$refs.observerTarget);
        },
        onScroll() {
            if (!this.ticking) {
                window.requestAnimationFrame(() => {
                    this.checkVisibility();
                    this.ticking = false;
                });
                this.ticking = true;
            }
        },
        checkVisibility() {
            const rect = this.$refs.observerTarget.getBoundingClientRect();
            this.isVisible = rect.bottom > -this.sensitivity * window.innerHeight && rect.top < (this.sensitivity + 1) * window.innerHeight;
        },
    },
};