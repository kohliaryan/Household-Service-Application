export default {
    params: ['id'],
    template: `
    <div>
        <h1> This is blog page </h1>
        {{$router.params.id}}
    </div>
    `
}