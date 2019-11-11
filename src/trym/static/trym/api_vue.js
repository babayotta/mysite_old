new Vue({
    el: '#starting',
    delimiters: ['${','}'],
    data: {
        table: [],
        loading: true,
        currentTransaction: {},
        message: null,
        newTransaction: {},
    },
    mounted: function() {
        this.getTable();
    },
    methods: {
        getTable: function() {
            let api_url = '/trym/api/transaction/get_table';
            this.loading = true;
            this.$http.get(api_url)
                .then((response) => {
                    this.table = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getTransactions: function() {
            let api_url = '/trym/api/transaction/';
            this.loading = true;
            this.$http.get(api_url)
                .then((response) => {
                    this.profit_transactions = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getTransaction: function(id) {
            this.loading = true;
            this.$http.get(`/trym/api/transaction/${id}/`)
                .then((response) => {
                    this.currentTransaction = response.data;
                    $("#editTransactionModal").modal('show');
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        addTransaction: function() {
            this.loading = true;
            this.$http.post('/trym/api/transaction/',this.newTransaction)
                .then((response) => {
                    this.loading = true;
                    this.getTransactions();
                })
                .catch((err) => {
                    this.loading = true;
                    console.log(err);
                })
        },
        update: function() {
            this.loading = true;
            this.$http.put(`/trym/api/transaction/${this.currentTransaction.id}/`, this.currentTransaction)
                .then((response) => {
                    this.loading = false;
                    this.currentTransaction = response.data;
                    this.getTransactions();
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        deleteTransaction: function(id) {
            this.loading = true;
            this.$http.delete(`/trym/api/transaction/${id}/`)
                .then((response) => {
                    this.loading = false;
                    this.getTransactions();
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        }
    }
});
 