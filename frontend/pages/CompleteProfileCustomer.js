export default {
    template: `
        <div class="container mt-5">
            <div class="card p-4 shadow">
                <h1 class="mb-4">Complete Your Profile</h1>
                <form>
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input type="text" id="name" class="form-control" placeholder="Enter your name" />
                    </div>
                    <div class="mb-3">
                        <label for="pincode" class="form-label">Pincode</label>
                        <input type="text" id="pincode" class="form-control" placeholder="Enter your pincode" />
                    </div>
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <textarea id="address" class="form-control" rows="3" placeholder="Enter your address"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Complete</button>
                </form>
            </div>
        </div>
    `
};
