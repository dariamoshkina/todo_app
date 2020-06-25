<template>
	<div class="container">
		<div class="row">
			<div class="col-sm-10">
				<h1>You have {{tasks.length}} tasks</h1>
				<table class="table table-hover">
					<thead>
						<tr>
							<th id="description-column" @click="sort('description', $event)" class="th-sm">Description</th>
							<th id="priority_id-column" @click="sort('priority_id', $event)" class="th-sm">Priority</th>
							<th id="created_at-column" @click="sort('created_at', $event)" class="th-sm">Created at</th>
							<th class="table-button"/>
							<th class="table-button"/>
						</tr>
					</thead>
					<tbody>
						<Task v-for="task in sortedTasks" :key="task.task_id" v-bind:task="task" />
					</tbody>
				</table>
				<br>
				<AddTask />
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import Task from './Task';
import AddTask from './AddTask';

export default {
	name: 'Tasks',
	data() {
		return {
			tasks: [],
			currentSort: 'created_at',
			currentSortDir: 'asc'
		};
	},
	methods: {
		getTasks() {
			const path='http://127.0.0.1:5000/task';
			axios.get(path)
				.then((res) => {
					this.tasks = res.data;
				})
				.catch((error) => {
					console.error(error);
				});
		},
		sort(field, evt) {
			if (arguments.length === 1) {
				let sortHeader = document.getElementById(field+'-column');
				sortHeader.textContent += ' \u25BC';
			}
			else {
				if (field === this.currentSort) {
					this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
				} else {
					this.currentSortDir = 'asc';
				}
				let headers = ['description', 'priority_id', 'created_at'];
				headers.forEach(header => {
					let tableHeader = document.getElementById(header+'-column');
					tableHeader.textContent = tableHeader.textContent.replace(/\s{1}\u25BC|\u25B2/, '');
				});
				evt.target.textContent += this.currentSortDir === 'asc' ? ' \u25BC' : ' \u25B2';
			}
			this.currentSort = field;
		}
	},
	computed: {
		sortedTasks() {
			return this.tasks.slice().sort((a,b) => {
				let modifier = 1;
				if (this.currentSortDir === 'desc') modifier = -1;
				if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
				if (a[this.currentSort] > b[this.currentSort]) return modifier;
				return 0;
			});
		}
	},
	components: {
		Task,
		AddTask
	},
	created() {
		this.getTasks();
	},
	mounted() {
		this.currentSortDir = 'asc';
		this.sort('created_at');
	}
};
</script>

<style>
table {
	table-layout: fixed;
	word-wrap: break-word;
}
#description-column {
	width: 45%;
}
#priority-column {
	width: 15%;
}
#created_at-column {
	width: 20%;
}
.table-button {
	width: 10%;
}
</style>