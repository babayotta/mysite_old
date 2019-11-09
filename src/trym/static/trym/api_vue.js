new Vue({
    el: '#starting',
    delimiters: ['${','}'],
    data: {
        profit_transactions: [],
        tax_transactions: [],
        buy_transactions: [],
        loading: true,
        currentTransaction: {},
        message: null,
        newTransaction: {},
//        search_term: '',
    },
    mounted: function() {
        this.getProfitTransactions();
        this.getTaxTransactions();
        this.getBuyTransactions();
    },
    methods: {
        getProfitTransactions: function() {
            let api_url = '/trym/api/transaction/?transaction_type=P';
//            if(this.search_term!==''||this.search_term!==null) {
//                api_url = `/trym/api/transaction/?search=${this.search_term}`
//            }
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
        getTaxTransactions: function() {
            let api_url = '/trym/api/transaction/?transaction_type=T';
//            if(this.search_term!==''||this.search_term!==null) {
//                api_url = `/trym/api/transaction/?search=${this.search_term}`
//            }
            this.loading = true;
            this.$http.get(api_url)
                .then((response) => {
                    this.tax_transactions = response.data;
                    this.loading = false;
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        },
        getBuyTransactions: function() {
            let api_url = '/trym/api/transaction/?transaction_type=B';
 //           if(this.search_term!==''||this.search_term!==null) {
 //               api_url = `/trym/api/transaction/?search=${this.search_term}`
 //           }
            this.loading = true;
            this.$http.get(api_url)
                .then((response) => {
                    this.buy_transactions = response.data;
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
 