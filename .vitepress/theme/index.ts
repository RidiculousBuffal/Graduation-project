import DefaultTheme from "vitepress/theme";
import ThemeImage from "./components/ThemeImage.vue";
import GitCard from "./components/GitCard.vue";
import AttachmentDownload from "./components/AttachmentDownload.vue";
import './index.css'
export default {
    extends: DefaultTheme,
    enhanceApp({app}) {
        app.component('ThemeImage', ThemeImage)
        app.component('GitCard', GitCard)
        app.component('AttachmentDownload', AttachmentDownload)
    }
}