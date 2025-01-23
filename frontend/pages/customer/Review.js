export default {
    template: `
      <div class="container my-5">
        <h2 class="text-center text-primary mb-4">Review Page</h2>
        <div class="card shadow-lg p-4">
          <!-- Review Input Section -->
          <div class="form-group">
            <label for="reviewInput" class="font-weight-bold">Your Review:</label>
            <input 
              type="text" 
              id="reviewInput" 
              v-model="review" 
              class="form-control"
              placeholder="Write your review here..." 
            />
          </div>
          <button 
            @click="submitReview" 
            class="btn btn-primary mt-3"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? "Submitting..." : "Submit Review" }}
          </button>
  
          <!-- Feedback Section -->
          <div v-if="feedbackMessage" class="alert mt-3" :class="feedbackClass">
            {{ feedbackMessage }}
          </div>
        </div>
      </div>
    `,
    data() {
      return {
        review: "", // Stores the current review
        feedbackMessage: "", // Stores feedback messages for the user
        feedbackClass: "", // Bootstrap alert class based on success or error
        isSubmitting: false, // To prevent multiple submissions
      };
    },
    async mounted() {
      const requestId = this.$route.params.id; // Fetch the request ID dynamically
      try {
        const response = await fetch(`${location.origin}/api/review/${requestId}`, {
          headers: {
            Authorization: this.$store.state.auth_token,
          },
        });
  
        if (response.ok) {
          const data = await response.json();
          this.review = data.remark; // Populate review if it exists
        } else {
          this.feedbackMessage = "No existing review found.";
          this.feedbackClass = "alert-warning";
        }
      } catch (error) {
        console.error("Error fetching review:", error);
        this.feedbackMessage = "Failed to fetch the review. Please try again.";
        this.feedbackClass = "alert-danger";
      }
    },
    methods: {
      async submitReview() {
        if (this.isSubmitting) return;
        this.isSubmitting = true;
  
        const requestId = this.$route.params.id; // Dynamically get the request ID
        try {
          const response = await fetch(`${location.origin}/api/review/${requestId}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: this.$store.state.auth_token,
            },
            body: JSON.stringify({ remarks: this.review }),
          });
  
          if (response.ok) {
            this.feedbackMessage = "Review submitted successfully!";
            this.feedbackClass = "alert-success";
          } else {
            const error = await response.json();
            this.feedbackMessage = error.msg || "Failed to submit the review.";
            this.feedbackClass = "alert-danger";
          }
        } catch (error) {
          console.error("Error submitting review:", error);
          this.feedbackMessage = "An unexpected error occurred. Please try again.";
          this.feedbackClass = "alert-danger";
        } finally {
          this.isSubmitting = false; // Reset the button state
        }
      },
    },
  };
  