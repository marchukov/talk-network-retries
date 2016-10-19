R2575 = csvread('~/tmp/pyconcz2016-net-failures/gilbert_2575.csv');
R5050 = csvread('~/tmp/pyconcz2016-net-failures/gilbert_5050.csv');
R7525 = csvread('~/tmp/pyconcz2016-net-failures/gilbert_7525.csv');

% MB total per each 0.1 sec interval
A2575 = accumarray(floor(R2575(:,1) * 10) + 1, R2575(:,2)) / 10^6;
A5050 = accumarray(floor(R5050(:,1) * 10) + 1, R5050(:,2)) / 10^6;
A7525 = accumarray(floor(R7525(:,1) * 10) + 1, R7525(:,2)) / 10^6;


set(gcf,'PaperUnits','inches','PaperSize',[15,5],'PaperPosition',[0 0 15 5]);

subplot(3, 1, 1);
hold on;
bar(A2575, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
title('p = 0.25, r = 0.75', 'FontSize', 14);
xlabel('Time Intervals (0.1 sec)');
ylabel('MB');
grid();
axis('tic', 'labelxy');

subplot(3, 1, 2);
hold on;
bar(A5050, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
title('p = 0.5, r = 0.5', 'FontSize', 14);
xlabel('Time Intervals (0.1 sec)');
ylabel('MB');
grid();
axis('tic', 'labelxy');

subplot(3, 1, 3);
hold on;
bar(A7525, 'facecolor', [0.75,0.75,0.75], 'edgecolor', 'none');
title('p = 0.75, r = 0.25', 'FontSize', 14);
xlabel('Time Intervals (0.1 sec)');
ylabel('MB');
grid();
axis('tic', 'labelxy');

% print -dpng -r100 file.png
% convert file.png -trim file.png
