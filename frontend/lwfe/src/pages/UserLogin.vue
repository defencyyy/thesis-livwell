<!-- <template>
<div class="row">
    <div class="col-md-6 offset-md-3">
        <div>
        <div>
            <h3>Login{{firstname}}</h3>
            <hr>
        </div>
        <form>
            <div class="form-group">
            <label >Email</label>
            <input type="text" class="form-control" >
        </div>
        <div class="form-group">
            <label >Password</label>
            <input type="password" class="form-control" >
        </div>
        <div class="my-3">
            <button type="submit" class="btn btn-primary">Login</button>
        </div>
        </form>
    </div>
    </div>
</div>
</template>
<script>
import {mapState} from 'vuex';
export default {
    computed:{
        ...mapState('auth',{firstname: state=> state.name,}),
    },
};
</script> -->
<template>
  <form @submit.prevent="loginUser">
    <input v-model="username" placeholder="Username" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/token/login/', {
          username: this.username,
          password: this.password,
        });
        console.log('Login successful, token:', response.data); // Store the token as needed
        // Handle successful login (e.g., redirect or save token)
      } catch (error) {
        console.error('Login error:', error.response ? error.response.data : error.message);
      }
    },
  },
};
</script>
