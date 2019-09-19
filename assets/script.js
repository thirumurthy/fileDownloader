Vue.config.devtools = false;
Vue.config.productionTip = false;
console.clear();
new Vue({
  el: "#app",
  data() {
    return {
      rules: [
        value => !!value || 'Required.',
        value => (value || '').length >= 10 || 'Min 10 characters',
      ],
      search: "",
      rurl:"",
      alert : false,
      delalert : false,
      filename : "",
      totalDesserts: 0,
      desserts: [],
      loading: true,
      pagination: {},
      headers: [
      {
        text: "File Name",
        align: "left",
        sortable: false,
        value: "name" },

      { text: "Created Date", value: "ctime" },
      { text: "size", value: "size" },
      { text: "Action",value: 'action', sortable: false }
    
    ] };


  },
  watch: {
    params: {
      handler() {
        this.getDataFromApi().then(data => {
          console.log("GETDATA");
          this.desserts = data.items;
          this.totalDesserts = data.total;
        });
      },
      deep: true } },


  mounted() {
    this.getDataFromApi().then(data => {
      this.desserts = data.items;
      this.totalDesserts = data.total;
    });
  },

  computed: {
    params(nv) {
      return {
        ...this.pagination,
        query: this.search };

    } },


  methods: {
    downloadFile(item){
      console.log(item);
      window.open("/getfile/"+escape(item.name), "_blank")
    },
    deleteFile(item){
      this.loading = true;
      let URL = "/deletefile/"+ item.name;
      this.filename = item.name;
      let _self= this;
        axios.get(URL).then((response) => {
          console.log(response.data)
          if(response.data == "success"){
            _self.delalert  = true;
            setTimeout(() => {
              _self.getDataFromApi().then(data => {
                this.desserts = data.items;
                this.totalDesserts = data.total;
              });
              
            }, 300);
          }
          this.loading = false

        });
    },
    requestDownload(){
      this.loading = true;
      let URL = "/download/request?durl="+ this.rurl;
      let _self= this;
        axios.post( {
          method: 'post',
          url: URL,
          data:{ durl: this.rurl }}).then((response) => {
          console.log(response.data)
          if(response.data == "submitted"){
            _self.alert = true;
            setTimeout(() => {
              _self.getDataFromApi().then(data => {
                this.desserts = data.items;
                this.totalDesserts = data.total;
              });
              
            }, 300);
          }
          this.loading = false

        });
    },
    getDataFromApi() {
      this.loading = true;
      return new Promise((resolve, reject) => {
        let URL = "/getfileinfo";
        axios.get(URL).then((response) => {
          // console.log(response.data, this)
          let items =  response.data
          this.loading = false
          

          const {
            sortBy,
            descending,
            page,
            rowsPerPage } =
          this.pagination;
          let search = this.search.trim().toLowerCase();

          //let items = this.getDesserts();

          if (search) {
            items = items.filter(item => {
              return Object.values(item).
              join(",").
              toLowerCase().
              includes(search);
            });
          }

          if (this.pagination.sortBy) {
            items = items.sort((a, b) => {
              const sortA = a[sortBy];
              const sortB = b[sortBy];

              if (descending) {
                if (sortA < sortB) return 1;
                if (sortA > sortB) return -1;
                return 0;
              } else {
                if (sortA < sortB) return -1;
                if (sortA > sortB) return 1;
                return 0;
              }
            });
          }

          if (rowsPerPage > 0) {
            items = items.slice(
            (page - 1) * rowsPerPage,
            page * rowsPerPage);

          }

          const total = items.length;


          setTimeout(() => {
            this.loading = false;
            resolve({
              items,
              total });

          }, 300);
        }); // api data fetch
      });
    },
    getDesserts() {
      return [
      {
        value: false,
        name: "Frozen Yogurt",
        calories: 159,
        fat: 6.0,
        carbs: 24,
        protein: 4.0,
        iron: "1%" },

      {
        value: false,
        name: "Ice cream sandwich",
        calories: 237,
        fat: 9.0,
        carbs: 37,
        protein: 4.3,
        iron: "1%" },

      {
        value: false,
        name: "Eclair",
        calories: 262,
        fat: 16.0,
        carbs: 23,
        protein: 6.0,
        iron: "7%" },

      {
        value: false,
        name: "Cupcake",
        calories: 305,
        fat: 3.7,
        carbs: 67,
        protein: 4.3,
        iron: "8%" },

      {
        value: false,
        name: "Gingerbread",
        calories: 356,
        fat: 16.0,
        carbs: 49,
        protein: 3.9,
        iron: "16%" },

      {
        value: false,
        name: "Jelly bean",
        calories: 375,
        fat: 0.0,
        carbs: 94,
        protein: 0.0,
        iron: "0%" },

      {
        value: false,
        name: "Lollipop",
        calories: 392,
        fat: 0.2,
        carbs: 98,
        protein: 0,
        iron: "2%" },

      {
        value: false,
        name: "Honeycomb",
        calories: 408,
        fat: 3.2,
        carbs: 87,
        protein: 6.5,
        iron: "45%" },

      {
        value: false,
        name: "Donut",
        calories: 452,
        fat: 25.0,
        carbs: 51,
        protein: 4.9,
        iron: "22%" },

      {
        value: false,
        name: "KitKat",
        calories: 518,
        fat: 26.0,
        carbs: 65,
        protein: 7,
        iron: "6%" }];


    } } });