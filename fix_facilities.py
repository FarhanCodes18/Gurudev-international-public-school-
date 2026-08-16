content = open('index.html', encoding='utf-8').read()

# Fix the broken section-header-flex closing
old = '        <a href="campus.html" class="btn btn-outline">View All       <div class="facilities-grid">'
new = '        <a href="campus.html" class="btn btn-outline">View All <i class="fa-solid fa-arrow-right"></i></a>\n      </div>\n      <div class="facilities-grid">'
content = content.replace(old, new)

# Fix the broken end
old2 = '      </div>ght"></i></a>\n          </div>\n        </div>\n      </div>\n    </div>\n  </section>'
new2 = '      </div>\n    </div>\n  </section>'
content = content.replace(old2, new2)

open('index.html', 'w', encoding='utf-8').write(content)
print('Fixed!')
