/**
 * Sorts a HTML table
 * @param {HTMLTable} table The table to sort 
 * @param {number} column the index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending
 */


function sortTableByColumn(table, column, asc = true){
    const dirModifier = asc ? 1 : -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll("tr"));


    //sort each row
    
    const sortedRows = rows.sort((a,b) => {
        if(column==2|column==3|column==5|column==23){
            const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
            return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
        }else if(column==6|column==7|column==8|column==9|column==10|column==11|column==12|column==13|column==14|column==15|column==16|column==17|column==18|column==19){
            const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();;
            const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();;
            return parseInt(aColText) > parseInt(bColText) ? (-1 * dirModifier) : (1 * dirModifier);
        }else if(column==4|column==20){
            const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();;
            const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();;
            return parseInt(aColText) > parseInt(bColText) ? (1 * dirModifier) : (-1 * dirModifier);
        }else if(column==3){
            const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();;
            const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();;
            return aColText > bColText ? (-1 * dirModifier) : (1 * dirModifier);
        }
    });
   
    // Remove all existing TRs from the table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }
    //Re-add the newly sorted row
    
    tBody.append(...sortedRows);
   
    //Remember how the column is currently sorted
    table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc","th-sort-desc"));
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
    if(table.querySelector(`th:nth-child(${column + 1})`).classList == ('th-sort-asc')){
        $('table tbody tr td:first-child').html(function(i){
            return i+1 ;
        })
        $('table tbody tr td:nth-child(22)').html(function(i){
            return i+1;
        })
        //     console.log(i[0]+1);
        
    }
    table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
    
}

document.querySelectorAll(".table-sortable th").forEach(headerCell => {
    headerCell.addEventListener("mousedown",() => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");

        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});
