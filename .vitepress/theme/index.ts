import DefaultTheme from "vitepress/theme";
import ThemeImage from "./components/ThemeImage.vue";
import GitCard from "./components/GitCard.vue";

export default {
    extends: DefaultTheme,
    enhanceApp({app}) {
        app.component('ThemeImage', ThemeImage)
        app.component('GitCard', GitCard)
    }
}