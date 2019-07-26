<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
      <b-navbar-brand href="#">알파알렙성경</b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">
        <!-- <b-navbar-nav>
          <b-nav-item href="#">Link</b-nav-item>
          <b-nav-item href="#" disabled>Disabled</b-nav-item>
        </b-navbar-nav> -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="검색"/>
            <b-button size="sm" class="my-2 my-sm-0" type="submit">검색</b-button>
          </b-nav-form>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="row">

      <div class="col-md" id="text_div" style="padding-right:0px;">
        <div id="subNav_text">
          <div class="row">
            <div class="col-3">
              <b-form-select 
                v-model="verselected" 
                :options="verlist" 
                class="mb-3" 
                size="sm" 
                />              
            </div>
            <div class="col-3">
              <b-form-select 
                v-model="bookselected" 
                :options="booklist" 
                class="mb-3" 
                size="sm" 
                />              
            </div>
            <div class="col-2">
              <b-form-select 
                v-model="chpselected" 
                :options="chplist" 
                class="mb-3" 
                size="sm" 
                />              
            </div>
          </div>
        </div> 
        <div id="text">
          <div v-if="verselected==='bhs'">
            <!-- bhs 텍스트가 컴파일되어 들어가는 곳 -->
            <component :is="verse"></component>
          </div>
          <div v-else-if="verselected==='gnt'">
            <!-- gnt 텍스트가 컴파일되어 들어가는 곳 -->
            <component :is="verse"></component>
          </div>
          <div v-else>
            <ol>
              <li v-for="(value, key) in verse" class="verseView" v-bind:key='key'>
                {{ value }}
              </li>
            </ol>
          </div>
        </div>
      </div>

      <div class="col-md" id="result_div" style="padding-left:0px; padding-right:0px;">
        <div id="subNav_result">
          데이터 결과 메뉴
        </div>
        <div v-html="dataResult" id="dataResult">
          <!-- 데이터 분석 결과를 보여주는 곳 -->
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import BookData from '@/data/BookData'
import TextController from '@/controller/TextController'

export default {
  name: 'Main',
  data() {
    return {
      verse: {},
      booklist: [],
      chplist: [],
      verlist: BookData.verlist,
      bookselected: 'Genesis',
      chpselected: 1,
      verselected: 'kor',
      dataResult: '데이터 결과 들어가는 곳'
    }
  },
  methods: {

  },
  mounted: async function() {
    TextController.updateText(this, 0) 
    this.booklist = BookData.old_booklist.concat(BookData.new_booklist)
  },
  watch: {
    bookselected: async function() {
      TextController.updateText(this, 1)
    },
    chpselected: async function() {
      TextController.updateText(this, 0)
    },
    verselected: async function() {
    // 이미 신약이 선택되어 있는 상태에서 bhs를 선택하면 창세기로 구약이 선택되어 있는 상태에서 
    // gnt를 선택하면 마태복음으로..
      if(this.verselected == 'gnt') {
        if(BookData.new_booklist.map(x => x.value).indexOf(this.bookselected)==-1) {
          this.bookselected = 'Matthew'
        }
        this.booklist = BookData.new_booklist
      }
      else if(this.verselected == 'bhs') {
        if(BookData.old_booklist.map(x => x.value).indexOf(this.bookselected)==-1) {
          this.bookselected = 'Genesis'
        }
        this.booklist = BookData.old_booklist
      }
      else {
        this.booklist = BookData.old_booklist.concat(BookData.new_booklist)
      }
      TextController.updateText(this, 0)
    }
  } 
}

// gnt를 선택했을 때는 구약을, bhs를 선택했을 때 신약을 접근하지 못하게 하는 로직 필요함. 
</script>