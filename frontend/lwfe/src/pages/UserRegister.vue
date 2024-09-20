<!-- <template>
<div class="row">
    <div class="col-md-6 offset-md-3">
        <div>
        <div>
            <h3>Register</h3>
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
            <button type="submit" class="btn btn-primary">Register</button>
        </div>
        </form>
    </div>
    </div>
</div>
</template>
<script>
export default {};
</script> -->
<template>
  <form @submit.prevent="registerUser">
    <input v-model="username" placeholder="Username" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Register</button>
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
    async registerUser() {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/users/', {
          username: this.username,
          password: this.password,
        });
        console.log('User registered:', response.data);
        // Handle successful registration (e.g., redirect or show a message)
      } catch (error) {
        console.error('Registration error:', error.response ? error.response.data : error.message);
      }
    },
  },
};
</script>
