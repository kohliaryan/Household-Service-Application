export default {
    props: ['id'],
    template: `
    <div class="container my-5">
      <h2 class="text-center text-primary mb-4">Professionals</h2>
      <div class="row">
        <div 
          v-for="professional in professionals" 
          :key="professional.id" 
          class="col-md-6 col-lg-4 mb-4">
          <div class="card shadow-lg">
            <div class="card-body">
              <h5 class="card-title text-success">{{ professional.name }}</h5>
              <p class="card-text">
                <strong>Address:</strong> {{ professional.address }}<br>
                <strong>Pincode:</strong> {{ professional.pincode }}<br>
                <strong>Experience:</strong> {{ professional.experience }}<br>
                <strong>Description:</strong> {{ professional.description }}
              </p>
              <button 
                @click="$router.push('/professional/' + professional.id)" 
                class="btn btn-outline-primary btn-block">
                Book Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
    data(){
        return {
            professionals: [],
        }
    },

    async mounted(){
        const res = await fetch(`${location.origin}/api/prof/${this.id}`, {
            headers : {
                'Authorization' : this.$store.state.auth_token
            }
        })
        if (res.ok){
            this.professionals = await res.json()
        }
    }
}