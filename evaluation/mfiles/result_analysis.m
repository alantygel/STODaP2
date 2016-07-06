close all; clear all;
% //task : water, budget, proc
% //method: ex, sto, free
results;

close all
h = figure(1);
bars = [median(tct{1}) median(tct{2}) median(tct{3}) median([tct{1} tct{2} tct{3}]);
		median(tct{4}) median(tct{5}) median(tct{6}) median([tct{4} tct{5} tct{6}]);
		median(tct{7}) median(tct{8}) median(tct{9}) median([tct{7} tct{8} tct{9}])];
bar(bars')
set (gca, 'XTickLabel', {'Water', 'Budget', 'Procurement', 'Aggregate'}) 
xlabel ('Tasks')
ylabel ('seconds')
% legend(h,,'location','Northwest')
grid
W = 4; H = 3;
set(h,'PaperUnits','inches')
set(h,'PaperOrientation','portrait');
set(h,'PaperSize',[H,W])
set(h,'PaperPosition',[0,0,W,H])

FN = findall(h,'-property','FontName');
set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
FS = findall(h,'-property','FontSize');
set(FS,'FontSize',8);

g = legend ('Exversion','STODaP','Free');
legend (g, 'location', 'Northwest');
% set (g, 'fontsize', 8);
legend boxoff

print(h,'-dpng','-color','~/Dropbox/Alan - Doutorado/Tese Text/tese/images/tct.png')
% 

close all
h = figure(1);
bars = [mean(accept{1}) mean(accept{2}) mean(accept{3}) mean([accept{1} accept{2} accept{3}]);
		mean(accept{4}) mean(accept{5}) mean(accept{6}) mean([accept{4} accept{5} accept{6}]);
		mean(accept{7}) mean(accept{8}) mean(accept{9}) mean([accept{7} accept{8} accept{9}])];
bar(bars')
set (gca, 'xticklabel', {'Q1:Water', 'Q2:Budget', 'Q3:Procurement','Aggregated'}) 
xlabel ('Tasks')
ylabel('Precision (%) ')
grid
W = 4; H = 3;
set(h,'PaperUnits','inches')
set(h,'PaperOrientation','portrait');
set(h,'PaperSize',[H,W])
set(h,'PaperPosition',[0,0,W,H])

FN = findall(h,'-property','FontName');
set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
FS = findall(h,'-property','FontSize');
set(FS,'FontSize',8);

g = legend ('Exversion','STODaP','Free');
legend (g, 'location', 'Northoutside');
% set (g, 'fontsize', 8);

legend boxoff
axis([.4 4.6 0 110])

% print(h,'-dpng','-color','./tct_bar.png')
print(h,'-dpng','-color','~/Dropbox/Alan - Doutorado/Tese Text/tese/images/precision.png')
% 
