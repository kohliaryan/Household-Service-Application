export default {
    template: `
        <div class="container mt-5">
            <div class="card p-4 shadow">
                <h1 class="mb-4">Service Profile Form</h1>
                <form>
                    <!-- Name -->
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" id="name" class="form-control" placeholder="Enter your name" />
                    </div>

                    <!-- Pincode -->
                    <div class="mb-3">
                        <label for="pincode" class="form-label">Pincode</label>
                        <input type="text" id="pincode" class="form-control" placeholder="Enter your pincode" />
                    </div>

                    <!-- Address -->
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <textarea id="address" class="form-control" rows="2" placeholder="Enter your address"></textarea>
                    </div>

                    <!-- Experience -->
                    <div class="mb-3">
                        <label for="experience" class="form-label">Experience (in years)</label>
                        <input type="number" id="experience" class="form-control" placeholder="Enter your experience" />
                    </div>

                    <!-- Description -->
                    <div class="mb-3">
                        <label for="description" class="form-label">Description</label>
                        <textarea id="description" class="form-control" rows="3" placeholder="Describe your services"></textarea>
                    </div>

                    <!-- Service ID -->
                    <div class="mb-3">
                        <label for="service_id" class="form-label">Service ID</label>
                        <input type="text" id="service_id" class="form-control" placeholder="Enter your service ID" />
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="btn btn-primary w-100">Submit</button>
                </form>
            </div>
        </div>
    `
};
