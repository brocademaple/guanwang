document.addEventListener('DOMContentLoaded', function () {
    const exportData = JSON.parse(document.getElementById('export-data').textContent);

    if (exportData && exportData.length > 0) {
        // 创建弹窗
        const modal = document.createElement('div');
        modal.style.position = 'fixed';
        modal.style.top = '50%';
        modal.style.left = '50%';
        modal.style.transform = 'translate(-50%, -50%)';
        modal.style.backgroundColor = 'white';
        modal.style.padding = '20px';
        modal.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.5)';
        modal.style.zIndex = '1000';

        const content = exportData.map(item => `
            <div>
                <strong>名称:</strong> ${item.name}<br>
                <strong>性别:</strong> ${item.gender}<br>
                <strong>修复类型:</strong> ${item.repair_type_display}<br>
                <strong>修复建议:</strong> ${item.diagnosis_data}<br>
                <strong>方案:</strong> ${item.scheme}<br>
            </div>
            <hr>
        `).join('');

        modal.innerHTML = `
            <h2>选中记录</h2>
            ${content}
            <button id="close-modal">关闭</button>
        `;

        document.body.appendChild(modal);

        // 关闭弹窗事件
        document.getElementById('close-modal').onclick = function () {
            document.body.removeChild(modal);
        };
    }
});