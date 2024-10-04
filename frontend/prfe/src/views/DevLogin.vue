<template>
    <div>
        <h2>Dev Login Page</h2>
        <form @submit.prevent="login">
            <div>
                <label for="username">Username:</label>
                <input type="text" v-model="username" id="username" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" v-model="password" id="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        };
    },
    methods: {
        login() {
            // Temporary logic: You can add your backend API call here later
            if (this.username && this.password) {
                this.$router.push('/devmain'); // Route to main page
            } else {
                alert("Please fill in both fields.");
            }
        }
    }
};
</script>
