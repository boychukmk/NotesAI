import { createRouter, createWebHistory } from 'vue-router';
import NotesList from '../views/NotesList.vue';
import NoteDetails from '../views/NoteDetails.vue';
import NoteForm from '../views/NoteForm.vue';
import Analytics from '../views/Analytics.vue';

const routes = [
    { path: '/', component: NotesList },
    { path: '/note/:id', component: NoteDetails, props: true },
    { path: '/create', component: NoteForm },
    { path: '/edit/:id', component: NoteForm, props: true },
    { path: '/analytics', component: Analytics },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
