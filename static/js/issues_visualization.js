(() => {
    const box = document.getElementById('complaints')
    const problemsUrl = box.dataset.url
    const issuesUrl = box.dataset.issuesUrl
    const prefix = box.dataset.prefix
    const other = JSON.parse(box.dataset.otherCategories || '[]')
    const total = document.getElementById(`id_${prefix}-TOTAL_FORMS`)

    const sync = async (catSel, keep = false) => {
        const row = catSel.closest('.complaint-row')
        const pWrap = row.querySelector('.problem-wrap')
        const cWrap = row.querySelector('.custom-wrap')
        const pSel = pWrap.querySelector('select')
        const val = catSel.value
        if (!val) { pWrap.hidden = cWrap.hidden = true; return }
        if (other.includes(Number(val))) {
            pWrap.hidden = true; cWrap.hidden = false
            pSel.innerHTML = '<option value=""></option>'
            return
        }
        cWrap.hidden = true; pWrap.hidden = false
        if (keep && pSel.options.length > 1) return;
        const { problems } = await (await fetch(`${problemsUrl}?category=${val}`)).json()
        pSel.innerHTML = '<option value=""></option>' +
            problems.map(p => `<option value="${p.id}">${p.name}</option>`).join('')
    }

    const addRow = () => {
        const i = Number(total.value)
        box.insertAdjacentHTML('beforeend', document.getElementById('empty-form').innerHTML.replaceAll("__prefix__", i))
        total.value = i + 1
        return box.lastElementChild
    }

    box.addEventListener('change', e => {
        if (e.target.name && e.target.name.endsWith('-category')) sync(e.target)
    })
    box.querySelectorAll("select[name$='-category']").forEach(s => { if (s.value) sync(s, true) })

    document.getElementById('add-row').addEventListener('click', addRow)

    if (issuesUrl) {
        const acc = document.getElementById('id_accepted_car')
        acc && acc.addEventListener('change', async () => {
            if (!acc.value) return
            const { issues } = await (await fetch(`${issuesUrl}?accepted=${acc.value}`)).json()
            box.querySelectorAll('.complaint-row').forEach(r => r.remove())
            total.value = 0
            for (const it of issues) {
                const row = addRow()
                const cat = row.querySelector("select[name$='-category']")
                cat.value = it.category
                await sync(cat)
                if (it.is_other) row.querySelector('.custom-wrap textarea').value = it._other_issue
                else if (it.problem) row.querySelector('.problem-wrap select').value = it.problem
            }
        })
    }
})()