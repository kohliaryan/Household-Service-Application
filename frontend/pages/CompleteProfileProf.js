export default {
    template: `
      <div class="container mt-5">
        <div class="card p-4 shadow">
          <h1 class="mb-4">Service Profile Form</h1>
          <form @submit.prevent="completeProfessionalProfile">
            <!-- Name -->
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input
                type="text"
                id="name"
                class="form-control"
                placeholder="Enter your name"
                v-model="name"
                required
              />
            </div>
  
            <!-- Pincode -->
            <div class="mb-3">
              <label for="pincode" class="form-label">Pincode</label>
              <input
                type="text"
                id="pincode"
                class="form-control"
                placeholder="Enter your pincode"
                v-model="pincode"
                required
              />
            </div>
  
            <!-- Address -->
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <textarea
                id="address"
                class="form-control"
                rows="2"
                placeholder="Enter your address"
                v-model="address"
                required
              ></textarea>
            </div>
  
            <!-- Experience -->
            <div class="mb-3">
              <label for="experience" class="form-label">Experience (in years)</label>
              <input
                type="number"
                id="experience"
                class="form-control"
                placeholder="Enter your experience"
                v-model="experience"
                required
              />
            </div>
  
            <!-- Description -->
            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea
                id="description"
                class="form-control"
                rows="3"
                placeholder="Describe your services"
                v-model="description"
                required
              ></textarea>
            </div>
  
            <!-- Service ID -->
            <div class="mb-3">
              <label for="service_id" class="form-label">Service ID</label>
              <input
                type="text"
                id="service_id"
                class="form-control"
                placeholder="Enter your service ID"
                v-model="service_id"
                required
              />
            </div>
  
            <!-- Submit Button -->
            <button type="submit" class="btn btn-primary w-100">Submit</button>
          </form>
        </div>
      </div>
    `,
    data() {
      return {
        name: null,
        pincode: null,
        address: null,
        experience: null,
        description: null,
        service_id: null,
      };
    },
    computed: {
      authToken() {
        return this.$store.state.auth_token;
      },
      userId() {
        return this.$store.state.user_id;
      },
    },
    methods: {
      async completeProfessionalProfile() {
        try {
          // Build the payload
          const payload = {
            user_id: this.userId,
            name: this.name,
            pincode: this.pincode,
            address: this.address,
            experience: this.experience,
            description: this.description,
            service_id: this.service_id,
          };
  
          // Make the API call
          const response = await fetch(`${location.origin}/api/profComplete`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.authToken}`, // Include token for authentication
            },
            body: JSON.stringify(payload),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert("Profile completed successfully!");
            // Redirect to professional dashboard or another page
            this.$router.push("/professionalDashboard");
          } else {
            alert(data.message || "Failed to complete the profile.");
          }
        } catch (error) {
          console.error("Error completing professional profile:", error);
          alert("An error occurred. Please try again later.");
        }
      },
    },
  };
  